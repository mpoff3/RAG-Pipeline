"use client";
import { useState } from "react";
import Upload from "../components/Upload";
import Chat from "../components/Chat";
import DocumentList from "../components/DocumentList";

export default function Home() {
  const [refreshDocs, setRefreshDocs] = useState<number>(0);

  const handleUploadSuccess = (): void => {
    setRefreshDocs(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">RAG in Action</h1>
        </div>
      </header>
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Left column - Upload and Documents */}
          <div className="lg:w-1/2 lg:flex-1">
            <Upload onUpload={handleUploadSuccess} />
            <DocumentList onRefresh={refreshDocs} />
          </div>
          
          {/* Right column - Chat */}
          <div className="lg:w-1/2 lg:flex-1">
            <Chat />
          </div>
        </div>
      </main>
    </div>
  );
} 