FROM node:22-alpine

WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# Copy the rest of the application
COPY . .

# Set environment variables for build time
ENV NEXT_TELEMETRY_DISABLED 1

# Build the Next.js application
RUN npm run build

# Google Cloud Run expects the app to listen on the $PORT environment variable.
ENV PORT 3000
EXPOSE 3000

CMD ["npm", "start"]
