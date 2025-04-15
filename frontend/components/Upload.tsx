"use client";
import React, { useRef, useState } from "react";

interface UploadProps {
  onUpload?: () => void;
}

export default function Upload({ onUpload }: UploadProps) {
  const fileInput = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [success, setSuccess] = useState<boolean>(false);

  async function handleUpload(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    setSuccess(false);
    const file = fileInput.current?.files?.[0];
    if (!file) {
      setError("Please select a PDF file.");
      return;
    }
    if (file.type !== "application/pdf") {
      setError("Only PDF files are allowed.");
      return;
    }
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append("files", file, file.name);
      const res = await fetch(process.env.NEXT_PUBLIC_BACKEND_URL + "/ingest", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Upload failed");
      }
      setSuccess(true);
      onUpload?.();
      if (fileInput.current) {
        fileInput.current.value = "";
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload error");
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">Upload a PDF file:</h2>
      <div className="bg-white shadow-sm border-2 border-dashed border-gray-300 rounded-lg p-6 hover:border-blue-400 transition-colors duration-200">
        <form className="flex flex-col gap-4" onSubmit={handleUpload}>
          <div className="relative">
            <input 
              type="file" 
              accept="application/pdf" 
              ref={fileInput} 
              className="block w-full text-gray-700 text-sm
                       file:mr-4 file:py-2 file:px-4 file:rounded-lg
                       file:border-0 file:text-sm file:font-medium
                       file:bg-blue-50 file:text-blue-700
                       hover:file:bg-blue-100 transition-all
                       cursor-pointer"
            />
          </div>
          <button 
            type="submit" 
            disabled={uploading}
            className="w-full bg-blue-600 text-white py-2.5 px-4 rounded-lg font-medium 
                     hover:bg-blue-700 active:bg-blue-800 
                     transition-all duration-200 shadow-sm
                     disabled:bg-gray-400 disabled:cursor-not-allowed
                     flex items-center justify-center gap-2"
          >
            {uploading ? (
              <>
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                </svg>
                Uploading...
              </>
            ) : (
              <>
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                Upload PDF
              </>
            )}
          </button>
        </form>
        {error && (
          <div className="mt-4 p-3 rounded-lg bg-red-50 text-red-600 text-sm flex items-center gap-2">
            <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
            </svg>
            {error}
          </div>
        )}
        {success && (
          <div className="mt-4 p-3 rounded-lg bg-green-50 text-green-600 text-sm flex items-center gap-2">
            <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
            </svg>
            Uploaded successfully!
          </div>
        )}
      </div>
    </div>
  );
} 