import React from "react";


const range = len => {
  const arr = [];
  for (let i = 0; i < len; i++) {
    arr.push(i);
  }
  return arr;
};

function newPerson(){
  const statusChance = Math.random();
  return {
    id: Math.floor(Math.random() * 10),
    techName:'TestName' ,
    phoneNumber: Math.floor(Math.random() * 10**8),
    location: 'Test Location',
    jobs: Math.floor(Math.random() * 10),
    status:
      statusChance > 0.66
        ? "active"
        : statusChance > 0.33 ? "inactive" : "review"
  };
};


export function makeData(len = 20) {
    const people =[]
    range(len).map(d => {
      people.push(newPerson())  
    });
    return {
        people
      };
  }