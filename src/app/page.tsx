"use client";

import Image from "next/image";
import { useState } from "react";

export default function Home() {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setSelectedImage(imageUrl);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-8 gap-16">
      <header className="text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">Visual Search Engine</h1>
        <p className="text-gray-500">Upload an image and find similar results</p>
      </header>

      <main className="flex flex-col items-center gap-6">
        {/* Image Upload Component */}
        <div className="flex flex-col items-center gap-4 border-2 border-dashed border-gray-400 p-6 rounded-lg">
          {selectedImage ? (
            <Image
              src={selectedImage}
              alt="Uploaded Preview"
              width={200}
              height={200}
              className="rounded-lg"
            />
          ) : (
            <p className="text-gray-500">Drag and drop or click to upload</p>
          )}
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            className="text-center cursor-pointer"
          />
        </div>

        {/* Example call to action */}
        <button
          className="bg-blue-600 text-white py-2 px-6 rounded-lg hover:bg-blue-700 transition"
          onClick={() => alert("Image submitted! Perform search logic here.")}
        >
          Search for Similar Images
        </button>
      </main>

      <footer className="text-center text-gray-500 text-sm mt-16">
        Made with Next.js and Tailwind CSS
      </footer>
    </div>
  );
}
