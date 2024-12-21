import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Import Routes instead of Switch
import GymSubscriptionPlanForm from './components/GymSubscriptionPlanForm';
import GymSubscriptionPlans from './components/GymSubscriptionPlans';
import GymReviewForm from './components/GymReviewForm';
import Gyms from './components/Gyms'; // New component for Gym list
import GymDetail from './components/GymDetail'; // New component for Gym details

function App() {
  return (
    <Router>
      <div className="App">
        <h1>Gym Management</h1>
        
        {/* Define your routes with Routes (instead of Switch) */}
        <Routes>
          <Route path="/" element={<Gyms />} /> {/* Home page with all gyms */}
          <Route path="/gyms/:gymId" element={<GymDetail />} /> {/* Gym details page */}
          <Route path="/subscription-plans" element={<GymSubscriptionPlans />} />
          <Route path="/subscription-plan-form" element={<GymSubscriptionPlanForm />} />
          <Route path="/review-form/:gymId" element={<GymReviewForm />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
