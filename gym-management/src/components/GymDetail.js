import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getRatings, getSubscriptionPlans, addReview, addRating } from '../api'; // API functions

const GymDetail = () => {
  const { gymId } = useParams(); // Use the gym ID from URL
  const [ratings, setRatings] = useState([]);
  const [subscriptionPlans, setSubscriptionPlans] = useState([]);
  const [reviewText, setReviewText] = useState('');
  const [ratingValue, setRatingValue] = useState(0);

  useEffect(() => {
    const fetchDetails = async () => {
      try {
        const ratingsData = await getRatings(gymId);
        setRatings(ratingsData);

        const subscriptionPlansData = await getSubscriptionPlans(gymId);
        setSubscriptionPlans(subscriptionPlansData);
      } catch (error) {
        console.error("Error fetching gym details", error);
      }
    };

    fetchDetails();
  }, [gymId]);

  const handleAddReview = async () => {
    try {
      const reviewData = {
        review: reviewText,
      };
      await addReview(gymId, reviewData);
      alert("Review added successfully");
      setReviewText('');
    } catch (error) {
      console.error("Error adding review", error);
    }
  };

  const handleAddRating = async () => {
    try {
      const ratingData = {
        rating: ratingValue,
      };
      await addRating(gymId, ratingData);
      alert("Rating added successfully");
    } catch (error) {
      console.error("Error adding rating", error);
    }
  };

  return (
    <div>
      <h2>Gym Details</h2>
      <div>
        <h3>Ratings</h3>
        <ul>
          {ratings.map((rating) => (
            <li key={rating.id}>
              <p>{rating.user}: {rating.rating} stars</p>
              <p>{rating.review}</p>
            </li>
          ))}
        </ul>
        <div>
          <input
            type="number"
            value={ratingValue}
            onChange={(e) => setRatingValue(e.target.value)}
            placeholder="Rate the gym"
          />
          <button onClick={handleAddRating}>Submit Rating</button>
        </div>
        <div>
          <textarea
            value={reviewText}
            onChange={(e) => setReviewText(e.target.value)}
            placeholder="Write a review"
          />
          <button onClick={handleAddReview}>Submit Review</button>
        </div>
      </div>

      <div>
        <h3>Subscription Plans</h3>
        <ul>
          {subscriptionPlans.map((plan) => (
            <li key={plan.id}>
              <p>{plan.plan_name}: ${plan.price}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default GymDetail;
