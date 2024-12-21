import React, { useState } from 'react';
import axios from 'axios';

const GymReviewForm = ({ gymId }) => {
  const [rating, setRating] = useState('');
  const [review, setReview] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    const data = {
      rating: rating,
      review: review,
    };

    axios.post(`/api/gym-rating-reviews/${gymId}/`, data)
      .then(response => {
        alert('Review submitted successfully');
      })
      .catch(error => {
        console.error('Error submitting review', error);
        alert('Failed to submit review');
      });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Rating:</label>
        <input
          type="number"
          value={rating}
          onChange={(e) => setRating(e.target.value)}
          min="1"
          max="5"
          required
        />
      </div>
      <div>
        <label>Review:</label>
        <textarea
          value={review}
          onChange={(e) => setReview(e.target.value)}
        ></textarea>
      </div>
      <button type="submit">Submit Review</button>
    </form>
  );
};

export default GymReviewForm;
