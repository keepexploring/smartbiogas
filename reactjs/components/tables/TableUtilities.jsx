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
    full_name:randomTextConstrucor(2) ,
    phone: Math.floor(Math.random() * 10**8),
    location: randomTextConstrucor(1),
    jobs_completed: Math.floor(Math.random() * 10),
    status:
      statusChance > 0.66
        ? "active"
        : statusChance > 0.33 ? "inactive" : "review"
  };
};

export function newJob(){
  const statusChance = Math.random();
  return {
    created_at:randomDateConstructor(Math.floor(Math.random() * 10**10)) ,
    id: Math.floor(Math.random() * 10),
    plant_id: Math.floor(Math.random() * 50),
    fault_description: randomTextConstrucor(6),
    fault_status:
      statusChance > 0.66
      ? "complete"
      : statusChance > 0.33 ? "overdue" : "resolving"
  };
};

export function detailsJob(){
  const statusChance = Math.random();
  return {
    id: Math.floor(Math.random() * 10),
    plant_id: Math.floor(Math.random() * 50),
    tech_id: Math.floor(Math.random() * 40),
    created_at:randomDateConstructor(Math.floor(Math.random() * 10**10)) ,
    overdue:randomDateConstructor(Math.floor(Math.random() * 10**10)) ,    
    fault_description: randomTextConstrucor(25),
    additional_info: testInfo,
    status:
      statusChance > 0.66
        ? "complete"
        : statusChance > 0.33 ? "overdue" : "resolving"
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
      full_name:randomTextConstrucor(2) ,
      phone: Math.floor(Math.random() * 10**8),
      address: Math.floor(Math.random() * 10) + ' ' + randomTextConstrucor(2),
      location: randomTextConstrucor(1),
      skills: randomTextConstrucor(3),
      languages: randomTextConstrucor(1),
      created_at:randomDateConstructor(dateNum),
      additional_info: testInfo,
      jobs_completed: Math.floor(Math.random() * 10),
      years_active: activeYears.toFixed(1),
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