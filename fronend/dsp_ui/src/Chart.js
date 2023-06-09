import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { useState, useEffect } from 'react';

const AuctionChart = () => {
  const [auctionData, setAuctionData] = useState([]);

  const addAuctionData = (data) => {
    const oldData = [...auctionData, data];
    setAuctionData(oldData);
  }

  useEffect(() => {
    // Fetch auction data from server every 5 seconds
    const interval = setInterval(() => {
      fetch('http://192.168.0.19/auction_data')
        .then(response => response.json())
        .then(data => addAuctionData(data));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <LineChart width={500} height={300} data={auctionData}>
      <XAxis dataKey="round" />
      <YAxis />
      <CartesianGrid strokeDasharray="3 3" />
      <Tooltip />
      <Line type="monotone" dataKey="budget" stroke="#8884d8" />
    </LineChart>
  );
};

export default AuctionChart;