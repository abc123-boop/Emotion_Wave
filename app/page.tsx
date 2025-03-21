"use client";

import type React from "react";
import UploadAudio from "../components/audio-uploader";
import { useState } from "react";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "../components/ui/tabs";
import { Button } from "../components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../components/ui/card";
import { Mic, Upload, Square } from "lucide-react";
import EmotionDisplay from "../components/emotion-display";
import MusicRecommendations from "../components/music-recommenations";
import AudioVisualizer from "../components/audio-visualizer";

export default function Home() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [detectedEmotion, setDetectedEmotion] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(
    null
  );
  const [audioChunks, setAudioChunks] = useState<Blob[]>([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      setMediaRecorder(recorder);

      const chunks: Blob[] = [];
      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunks.push(e.data);
        }
      };

      recorder.onstop = () => {
        const blob = new Blob(chunks, { type: "audio/webm" });
        const url = URL.createObjectURL(blob);
        setAudioBlob(blob);
        setAudioUrl(url);
        setAudioChunks([]);
      };

      setAudioChunks([]);
      recorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
      alert("Could not access your microphone. Please check permissions.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && isRecording) {
      mediaRecorder.stop();
      setIsRecording(false);
      // Release microphone access
      mediaRecorder.stream.getTracks().forEach((track) => track.stop());
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setAudioBlob(file);
      setAudioUrl(url);
    }
  };

  const detectEmotion = () => {
    if (!audioBlob) return;

    setIsProcessing(true);

    // Simulate emotion detection with a timeout
    // In a real app, you would send the audio to a backend API for processing
    setTimeout(() => {
      const emotions = ["happy", "sad", "angry", "neutral"];
      const detectedEmotion =
        emotions[Math.floor(Math.random() * emotions.length)];
      setDetectedEmotion(detectedEmotion);
      setIsProcessing(false);
    }, 2000);
  };

  return (
    <main className="container mx-auto py-8 px-4">
      <h1 className="text-4xl font-bold text-center mb-8">Emotion Detection</h1>

      <Tabs defaultValue="record" className="max-w-3xl mx-auto">
        <TabsList className="grid w-full grid-cols-2 mb-8">
          <TabsTrigger value="record">Record Voice</TabsTrigger>
          <TabsTrigger value="upload">Upload Audio</TabsTrigger>
        </TabsList>

        <TabsContent value="record">
          <Card>
            <CardHeader>
              <CardTitle>Record Your Voice</CardTitle>
              <CardDescription>
                Speak naturally and we'll detect your emotional state
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex justify-center">
                {isRecording ? (
                  <AudioVisualizer />
                ) : (
                  <div className="h-24 flex items-center justify-center">
                    <Mic size={64} className="text-muted-foreground" />
                  </div>
                )}
              </div>

              <div className="flex justify-center gap-4">
                {!isRecording ? (
                  <Button onClick={startRecording} className="gap-2">
                    <Mic size={16} />
                    Start Recording
                  </Button>
                ) : (
                  <Button
                    onClick={stopRecording}
                    variant="destructive"
                    className="gap-2"
                  >
                    <Square size={16} />
                    Stop Recording
                  </Button>
                )}
              </div>

              {audioUrl && (
                <div className="mt-4">
                  <p className="text-sm text-muted-foreground mb-2">Preview:</p>
                  <audio src={audioUrl} controls className="w-full" />
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="upload">
          <Card>
            <CardHeader>
              <CardTitle>Upload Audio File</CardTitle>
              <CardDescription>
                Upload an audio file to detect emotions
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-center w-full">
                <label
                  htmlFor="audio-upload"
                  className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed rounded-lg cursor-pointer bg-background hover:bg-accent/50"
                >
                  <div className="flex flex-col items-center justify-center pt-5 pb-6">
                    <Upload className="w-8 h-8 mb-3 text-muted-foreground" />
                    <p className="mb-2 text-sm text-muted-foreground">
                      <span className="font-semibold">Click to upload</span> or
                      drag and drop
                    </p>
                    <p className="text-xs text-muted-foreground">
                      MP3, WAV, or WEBM (max. 10MB)
                    </p>
                  </div>
                  <input
                    id="audio-upload"
                    type="file"
                    className="hidden"
                    accept="audio/*"
                    onChange={handleFileUpload}
                  />
                </label>
              </div>

              {audioUrl && (
                <div className="mt-4">
                  <p className="text-sm text-muted-foreground mb-2">Preview:</p>
                  <audio src={audioUrl} controls className="w-full" />
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {audioUrl && (
        <div className="max-w-3xl mx-auto mt-8">
          <Button
            onClick={detectEmotion}
            className="w-full"
            size="lg"
            disabled={isProcessing}
          >
            {isProcessing ? "Processing..." : "Detect Emotion"}
          </Button>
        </div>
      )}

      {detectedEmotion && (
        <div className="max-w-3xl mx-auto mt-8 space-y-8">
          <EmotionDisplay emotion={detectedEmotion} />
          <MusicRecommendations emotion={detectedEmotion} />
        </div>
      )}
    </main>
  );
}
