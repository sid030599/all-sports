# Step 1: Build the React app
FROM node:18 AS build

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the entire project into the container
COPY . .

# Build the React app for production
RUN npm run build

# Step 2: Set up the Nginx server to serve the app
FROM nginx:alpine

# Copy the build files from the build stage to the Nginx HTML folder
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 (the default port Nginx serves on)
EXPOSE 80

# Run Nginx in the foreground (required for Docker containers)
CMD ["nginx", "-g", "daemon off;"]
