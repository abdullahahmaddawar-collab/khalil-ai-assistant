/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@owl/component";

export class KhalilVoiceWidget extends Component {
    setup() {
        this.state = useState({ isRecording: false, transcript: "" });
    }

    async toggleRecording() {
        if (!this.state.isRecording) {
            this.startRecording();
        } else {
            this.stopRecording();
        }
    }

    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];

            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                await this.sendAudioToServer(audioBlob);
            };

            this.mediaRecorder.start();
            this.state.isRecording = true;
        } catch (err) {
            console.error("Microphone access denied or error:", err);
        }
    }

    stopRecording() {
        if (this.mediaRecorder) {
            this.mediaRecorder.stop();
            this.state.isRecording = false;
        }
    }

    async sendAudioToServer(blob) {
        const formData = new FormData();
        formData.append("audio", blob, "command.webm");

        try {
            // Local Flask server endpoint (Port 5001)
            const response = await fetch("http://localhost:5001/process-audio", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();
            this.state.transcript = data.result || "Processed successfully!";
        } catch (error) {
            console.error("Error sending audio to backend:", error);
        }
    }
}

KhalilVoiceWidget.template = "khalil_ai_assistant.VoiceWidgetTemplate";

// Odoo Systray mein widget register karna taake top bar par nazar aaye
export const systrayItem = {
    Component: KhalilVoiceWidget,
};

registry.category("systray").add("khalil_voice_assistant.widget", systrayItem, { sequence: 1 });