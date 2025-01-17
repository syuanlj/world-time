import React, { useState, useEffect } from 'react';
import './Clock.css';

function Clock({ cityName, timeZone }) {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const getTimeInTimeZone = () => {
    const options = { timeZone, hour12: false };
    const timeStr = time.toLocaleString('en-US', options);
    return new Date(timeStr);
  };

  const timeInZone = getTimeInTimeZone();
  
  const hours = timeInZone.getHours() % 12;
  const minutes = timeInZone.getMinutes();
  const seconds = timeInZone.getSeconds();

  const hourDegrees = ((hours * 30) + (minutes / 2)) + 180;
  const minuteDegrees = (minutes * 6) + 180;
  const secondDegrees = (seconds * 6) + 180;

  const renderHourMarks = () => {
    return Array.from({ length: 12 }, (_, i) => {
      const rotation = -(i * 30) + 180;
      return (
        <div
          key={i}
          className="hour-mark"
          style={{
            transform: `rotate(${rotation}deg)`
          }}
        >
          <span style={{ transform: `rotate(-${rotation}deg)` }}>
            {i === 0 ? '12' : i}
          </span>
        </div>
      );
    });
  };

  const renderMinuteMarks = () => {
    return Array.from({ length: 60 }, (_, i) => {
      const rotation = (i * 6);
      const isHourMark = i % 5 === 0;
      const hourNumber = i / 5;
      return (
        <div
          key={i}
          className={isHourMark ? "hour-tick" : "minute-mark"}
          style={{
            transform: `rotate(${rotation}deg)`
          }}
        >
          {isHourMark && (
            <span className="hour-number" style={{ transform: `rotate(-${rotation}deg)` }}>
              {hourNumber === 0 ? '12' : hourNumber}
            </span>
          )}
        </div>
      );
    });
  };

  return (
    <div className="clock-container">
      <div className="city-name">{cityName}</div>
      <div className="clock-face">
        {renderMinuteMarks()}
        {renderHourMarks()}
        <div
          className="hour-hand"
          style={{
            transform: `rotate(${hourDegrees}deg)`
          }}
        />
        <div
          className="minute-hand"
          style={{
            transform: `rotate(${minuteDegrees}deg)`
          }}
        />
        <div
          className="second-hand"
          style={{
            transform: `rotate(${secondDegrees}deg)`
          }}
        />
        <div className="center-dot" />
      </div>
      <div className="digital-time">{timeInZone.toLocaleTimeString('zh-CN', { timeZone })}</div>
    </div>
  );
}

export default Clock;