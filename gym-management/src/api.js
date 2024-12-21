import axios from 'axios';

const API_URL = "http://localhost:8000"; // Your backend URL, change if needed

// Set up an axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Fetch all gyms
export const getGyms = async () => {
  try {
    const response = await api.get("/gyms/");
    return response.data;
  } catch (error) {
    console.error("Error fetching gyms", error);
    throw error;
  }
};

// Add a new review for a gym
export const addReview = async (gymId, reviewData) => {
  try {
    const response = await api.post(`/gyms/${gymId}/reviews/`, reviewData);
    return response.data;
  } catch (error) {
    console.error("Error adding review", error);
    throw error;
  }
};

// Fetch subscription plans for a gym
export const getSubscriptionPlans = async (gymId) => {
  try {
    const response = await api.get(`/gyms/${gymId}/subscription_plans/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching subscription plans", error);
    throw error;
  }
};

// Add a new subscription plan
export const addSubscriptionPlan = async (gymId, planData) => {
  try {
    const response = await api.post(`/gyms/${gymId}/subscription_plans/`, planData);
    return response.data;
  } catch (error) {
    console.error("Error adding subscription plan", error);
    throw error;
  }
};

// Fetch ratings for a gym
export const getRatings = async (gymId) => {
  try {
    const response = await api.get(`/gyms/${gymId}/ratings_reviews/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching ratings", error);
    throw error;
  }
};

// Add rating for a gym
export const addRating = async (gymId, ratingData) => {
  try {
    const response = await api.post(`/gyms/${gymId}/ratings_reviews/`, ratingData);
    return response.data;
  } catch (error) {
    console.error("Error adding rating", error);
    throw error;
  }
};
