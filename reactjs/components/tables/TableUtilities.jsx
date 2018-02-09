import React from "react";

const range = len => {
  const arr = [];
  for (let i = 0; i < len; i++) {
    arr.push(i);
  }
  return arr;
};

export function newTechnician(){
  const statusChance = Math.random();
  return {
    id: Math.floor(Math.random() * 10),
    techName:randomTextConstrucor(2) ,
    techPhoneNumber: Math.floor(Math.random() * 10**8),
    techLocation: randomTextConstrucor(1),
    techJobs: Math.floor(Math.random() * 10),
    status:
      statusChance > 0.66
        ? "active"
        : statusChance > 0.33 ? "inactive" : "review"
  };
};

export function newJob(){
  const statusChance = Math.random();
  return {
    dateFlagged:randomDateConstructor(Math.floor(Math.random() * 10**10)) ,
    id: Math.floor(Math.random() * 10),
    plantID: Math.floor(Math.random() * 50),
    faultDescription: randomTextConstrucor(6),
    status:
      statusChance > 0.66
        ? "active"
        : statusChance > 0.33 ? "inactive" : "review"
  };
};

export function makeData(len,newEntry) {
    const people =[]
    range(len).map(d => {
      let entry = newEntry=='newJob'?newJob():newTechnician()
      people.push(entry)  
    });
    return {people}
    
  }

  const testInfo="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."  
  export function newProfile(){
    const statusChance = Math.random();
    const activeYears = Math.random()*10;
    const dateNum = Math.floor(Math.random() * 10**10)
    return {
      id: Math.floor(Math.random() * 10),
      techName:randomTextConstrucor(2) ,
      techPhoneNumber: Math.floor(Math.random() * 10**8),
      techAddress: Math.floor(Math.random() * 10) + ' ' + randomTextConstrucor(2),
      techLocation: randomTextConstrucor(1),
      techSkills: randomTextConstrucor(3),
      techLanguages: randomTextConstrucor(1),
      techStartDate:randomDateConstructor(dateNum),
      additionalInfo: testInfo,
      techJobsCompleted: Math.floor(Math.random() * 10),
      techYearsActive: activeYears.toFixed(1),
      status: statusChance > 0.66
      ? "active"
      : statusChance > 0.33 ? "inactive" : "review"
    }
  };

  function randomTextConstrucor(words){
    const randomText= "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
    const textArray =randomText.split(" ");
    let startKey=Math.floor(Math.random()*10);
    let valueText=''
    for(var i=0; i < words; i++ ){
       valueText=valueText+ ' ' + textArray[startKey+i]
    }
    return valueText;
  }

  function randomDateConstructor(num){
    const randomDate=new Date(num)
    return Date(randomDate)
  }