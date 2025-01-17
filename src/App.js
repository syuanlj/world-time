import React, { useState } from 'react';
import Clock from './components/Clock';
import './App.css';

function App() {
  const cities = [
    { name: '北京', timeZone: 'Asia/Shanghai' },
    { name: '伦敦', timeZone: 'Europe/London' },
    { name: '华盛顿', timeZone: 'America/New_York' },
    { name: '东京', timeZone: 'Asia/Tokyo' },
    { name: '悉尼', timeZone: 'Australia/Sydney' },
    { name: '巴黎', timeZone: 'Europe/Paris' },
    { name: '莫斯科', timeZone: 'Europe/Moscow' },
    { name: '柏林', timeZone: 'Europe/Berlin' },
    { name: '罗马', timeZone: 'Europe/Rome' },
    { name: '马德里', timeZone: 'Europe/Madrid' },
    { name: '开罗', timeZone: 'Africa/Cairo' },
    { name: '墨西哥城', timeZone: 'America/Mexico_City' },
    { name: '圣地亚哥', timeZone: 'America/Santiago' },
    { name: '布宜诺斯艾利斯', timeZone: 'America/Argentina/Buenos_Aires' },
    { name: '里约热内卢', timeZone: 'America/Sao_Paulo' },
    { name: '巴西利亚', timeZone: 'America/Brasilia' },
    { name: '多伦多', timeZone: 'America/Toronto' }
  ];

  const [selectedCity, setSelectedCity] = useState(cities[0]);

  return (
    <div className="App rustic">
      <h1 className="rustic-title">世界时钟</h1>
      <select 
        className="city-select"
        value={selectedCity.name}
        onChange={(e) => {
          const city = cities.find(c => c.name === e.target.value);
          setSelectedCity(city);
        }}
      >
        {cities.map(city => (
          <option key={city.name} value={city.name}>
            {city.name}
          </option>
        ))}
      </select>
      <div className="clock-grid rustic-grid">
        <Clock 
          cityName={selectedCity.name} 
          timeZone={selectedCity.timeZone} 
        />
      </div>
    </div>
  );
}

export default App;
