import React, { useState, useEffect } from "react";
import RegistrationForm from "../components/RegistrationForm";
import "../css/lessons.scss";
import Header from "../components/Header";

const months = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sept",
  "Oct",
  "Nov",
  "Dec",
];

const formatAMPM = (date) => {
  let hours = date.getHours();
  let minutes = date.getMinutes();
  let ampm = hours >= 12 ? 'pm' : 'am';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
  let strTime = hours + ':' + minutes + ' ' + ampm;
  return strTime;
}

//format session's date
const formatSession = (index, id, session) => {
  let date = session.getDate();
  if (date <= 9) {
    date = "0" + date;
  }
  let time = formatAMPM(session);
  date = `${date} ${months[session.getMonth()]}`;
  let title = `${date} ${time}`;
  let dateTime = new Date(session.getTime());
  return { index, id, title, date, time, dateTime, selected: "" };
};

//Lessons main component
const Lessons = () => {
  const [sessions, setSessions] = useState([]); //info about available sessions
  const [selected, setSelected] = useState(-1); //index of selected session
  const [details, setDetails] = useState(""); //details about selected session
  const [selectedDateTime, setSelectedDateTime] = useState(null); //details about selected session datetime

  //toggle selected session
  const toggleItem = (index) => {
    let items = sessions;
    if (selected !== -1) {
      items[selected].selected = "";
    }
    items[index].selected = "selected";
    setSelected(index);
    setSelectedDateTime(items[index].dateTime);
    setSessions(items);
    setDetails(
      `You have requested a lesson for ${items[index].title} \n Please complete this form to reserve your lesson.`
    );
  };
  //Load sessions info.
  useEffect(() => {
    let items = [];
    let session = new Date();

    session.setDate(session.getDate() + 9);
    session.setHours(15);
    session.setMinutes(0);
    session.setSeconds(0);
    items.push(formatSession(0, "first", session));

    session.setDate(session.getDate() + 5);
    session.setHours(16);
    session.setMinutes(0);
    session.setSeconds(0);
    items.push(formatSession(1, "second", session));

    session.setDate(session.getDate() + 7);
    session.setHours(17);
    session.setMinutes(0);
    session.setSeconds(0);
    items.push(formatSession(2, "third", session));
    setSessions((prev) => [...prev, ...items]);
  }, []);

  return (
    <main className="main-lessons">
      <Header selected="lessons" />
      {
        //Component to process user info for registration.
      }
      <RegistrationForm
        selected={selected}
        details={details}
        dateTime={selectedDateTime}
      />
      <div className="lesson-title" id="title">
        <h2>Guitar lessons</h2>
      </div>
      <div className="lesson-instruction">
        Choose from one of our available lessons to get started.
      </div>
      <div className="lessons-container">
        <div className="lessons-img">
          <img src="/assets/img/lessons.png" alt="" />
        </div>
        <div id="sr-items" className="lessons-cards">
          {sessions.map((session) => (
            <div
              className={`lesson-card ${session.selected}`}
              key={session.index}
            >
              <div className="lesson-info">
                <h2 className="lesson-date">{session.date}</h2>
                <h4 className="lesson-time">{session.time}</h4>
              </div>
              <button
                className="lesson-book"
                id={session.id}
                onClick={() => toggleItem(session.index)}
              >
                Book now!
              </button>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
};

export default Lessons;
