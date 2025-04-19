/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',  // Enable static HTML export
  distDir: '.next',
  images: {
    unoptimized: true, // Required for static export
  },
  // Since we're serving from the same domain in production
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: '/api/:path*',
      },
    ]
  },
}

module.exports = nextConfig 