FROM node:18-alpine

# Set work directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy project
COPY . .

# Expose port
EXPOSE 3000

# Default command
CMD ["npm", "run", "dev"] 