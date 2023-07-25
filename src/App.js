import React, { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
  const [curlMessage, setCurlMessage] = useState("");
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await axios.get("http://localhost:5000/get_messages");
      setMessages(response.data);
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (curlMessage.trim()) {
      try {
        await axios.post("http://localhost:5000/", { curl_message: curlMessage }, {
          headers: { "Content-Type": "application/json" }
        });
        setCurlMessage("");
        fetchMessages(); // Refresh the messages after submitting
      } catch (error) {
        console.error("Error submitting message:", error);
      }
    }
  };

  return (
    <div>
      <h1>cURL Message Logger</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={curlMessage}
          onChange={(e) => setCurlMessage(e.target.value)}
          placeholder="Enter your cURL message here"
        />
        <br />
        <button type="submit">Submit</button>
      </form>
      <h2>Stored Messages</h2>
      <ul>
        {messages.map((message) => (
          <li key={message.timestamp}>
            {message.timestamp} - {message.curl_message}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default App;
