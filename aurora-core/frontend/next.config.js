/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.PUBLIC_API_URL,
  },
  experimental: {
    styledComponents: true,
  },
}

module.exports = nextConfig
