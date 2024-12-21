import React, { useEffect, useState } from 'react';
import { getGyms } from '../api'; // Import API utility function

const Gyms = () => {
  const [gyms, setGyms] = useState([]);

  useEffect(() => {
    const fetchGyms = async () => {
      try {
        const gymsData = await getGyms();
        setGyms(gymsData);
      } catch (error) {
        console.error("Error fetching gyms", error);
      }
    };

    fetchGyms();
  }, []);

  return (
    <div>
      <h2>Gyms</h2>
      <ul>
        {gyms.map((gym) => (
          <li key={gym.id}>
            <h3>{gym.name}</h3>
            <p>{gym.location}</p>
            <button onClick={() => alert(`Show details for ${gym.name}`)}>View Details</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Gyms;
