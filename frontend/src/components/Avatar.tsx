"use client";

import Image from "next/image";

type AvatarProps = {
  src?: string | null;
  alt?: string;
  size?: number;
};

export default function Avatar({ src, alt = "User avatar", size = 48 }: AvatarProps) {
  return src ? (
    <Image
      src={src}
      alt={alt}
      width={size}
      height={size}
      className="rounded-full object-cover"
    />
  ) : (
    <div
      className="flex items-center justify-center rounded-full bg-gray-300 text-gray-600 font-bold"
      style={{ width: size, height: size }}
    >
      {alt?.charAt(0).toUpperCase()}
    </div>
  );
}
