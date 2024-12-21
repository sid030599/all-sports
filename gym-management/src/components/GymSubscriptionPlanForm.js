import React, { useState, useEffect } from 'react';
import axios from 'axios';

const GymSubscriptionPlanForm = () => {
  const [plans, setPlans] = useState([]);
  const [features, setFeatures] = useState([]);
  const [planName, setPlanName] = useState('');
  const [price, setPrice] = useState('');
  const [selectedFeatures, setSelectedFeatures] = useState([]);
  const [offers, setOffers] = useState('');

  // Fetching available gym features
  useEffect(() => {
    axios.get('/api/gym-features/')
      .then(response => setFeatures(response.data))
      .catch(error => console.error('Error fetching features', error));
  }, []);

  // Handle form submission for creating a subscription plan
  const handleSubmit = (e) => {
    e.preventDefault();
    const data = {
      plan_name: planName,
      price: price,
      features: selectedFeatures,
      offers: offers,
    };

    axios.post('/api/gym-subscription-plans/', data)
      .then(response => {
        alert('Subscription plan added successfully');
        setPlans([...plans, response.data]);
      })
      .catch(error => {
        console.error('Error adding subscription plan', error);
        alert('Failed to add subscription plan');
      });
  };

  return (
    <div>
      <h2>Create Gym Subscription Plan</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Plan Name:</label>
          <input
            type="text"
            value={planName}
            onChange={(e) => setPlanName(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Price:</label>
          <input
            type="number"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Features:</label>
          <select
            multiple
            value={selectedFeatures}
            onChange={(e) => setSelectedFeatures(Array.from(e.target.selectedOptions, option => option.value))}
            required
          >
            {features.map((feature) => (
              <option key={feature.id} value={feature.id}>
                {feature.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Offers:</label>
          <input
            type="text"
            value={offers}
            onChange={(e) => setOffers(e.target.value)}
          />
        </div>
        <button type="submit">Create Plan</button>
      </form>

      <h2>Existing Subscription Plans</h2>
      <ul>
        {plans.map(plan => (
          <li key={plan.id}>{plan.plan_name} - ${plan.price}</li>
        ))}
      </ul>
    </div>
  );
};

export default GymSubscriptionPlanForm;
