"use client";
import React, { useEffect, useState } from "react";

interface DocumentListProps {
  onRefresh?: number;
}

export default function DocumentList({ onRefresh }: DocumentListProps) {
  const [documents, setDocuments] = useState<string[]>([]);
  const [error, setError] = useState<string>("");
  const [deleting, setDeleting] = useState<string | null>(null);

  async function fetchDocuments() {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/documents`);
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to fetch documents");
      }
      const data = await res.json();
      setDocuments(data.documents || []);
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error loading documents");
    }
  }

  async function handleDelete(filename: string) {
    try {
      setDeleting(filename);
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/documents/${encodeURIComponent(filename)}`, {
        method: "DELETE",
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to delete document");
      }
      await fetchDocuments();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error deleting document");
    } finally {
      setDeleting(null);
    }
  }

  useEffect(() => {
    fetchDocuments();
  }, [onRefresh]);

  if (error) return (
    <div className="mb-6">
      <div className="text-red-600 bg-red-50 p-3 rounded-lg text-sm flex items-center gap-2">
        <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
        </svg>
        {error}
      </div>
    </div>
  );

  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">Uploaded Documents</h2>
      <div className="bg-white shadow-sm border border-gray-200 rounded-lg overflow-hidden">
        {documents.length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            No documents uploaded yet.
          </div>
        ) : (
          <ul className="divide-y divide-gray-200">
            {documents.map((doc, index) => (
              <li key={index} className="flex items-center justify-between p-4 hover:bg-gray-50 transition-colors duration-150">
                <span className="text-gray-700 font-medium truncate flex-1 mr-4">{doc}</span>
                <button
                  onClick={() => handleDelete(doc)}
                  disabled={deleting === doc}
                  className="px-3 py-2 text-sm font-medium text-white bg-red-500 rounded-md
                           hover:bg-red-600 active:bg-red-700 transition-colors duration-150
                           disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  {deleting === doc ? (
                    <>
                      <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                      </svg>
                      Deleting...
                    </>
                  ) : (
                    <>
                      <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                      Delete
                    </>
                  )}
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
} 