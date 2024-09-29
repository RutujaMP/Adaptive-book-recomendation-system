import React, { useState, useEffect } from 'react';
import { Typography, Button, Grid, Paper, Dialog, DialogTitle, DialogContent, DialogActions,Backdrop } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import adventorous from '../images/adventorous.jpg'
import cozy from "../images/cozy.jpg"
import funny from "../images/funny.jpg"
import happy2 from "../images/happy2.jpg"
import love from "../images/love.jpg"
import mysterious from "../images/mysterious.jpg"
import sad from "../images/sad.jpg"
import spring from "../images/spring.jpg"
import thought_provoking from "../images/thought provoking.jpg"
import axios from 'axios';
import { CircularProgress} from '@mui/material';


const HomePage = () => {
  const navigate = useNavigate();
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [mood, setMood] = useState('');
  const [suggestedGenre, setSuggestedGenre] = useState('');
  const [open, setOpen] = useState(false);
  const [selectedImages, setSelectedImages] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);


  // Function to open the dialog
  const handleClickOpen = () => {
    setOpen(true);
  };

  // Function to close the dialog
  const handleClose = () => {
    setOpen(false);
    axios.post(`http://127.0.0.1:8000/BookABook/get_mood_recommendations/`, {"mood_keywords" : selectedImages}).then((result) => 
    {
      console.log(result)
      const response = result.data
      navigate('/recommendations',  { state: { books : response } })
    }
  )
  };

  // Function to handle image selection
  const handleImageSelect = (imageName) => {
    if (selectedImages.includes(imageName)) {
      setSelectedImages(selectedImages.filter(img => img !== imageName));
    } else {
      if (selectedImages.length < 3) {
        setSelectedImages([...selectedImages, imageName]);
      }
    }
  };

  // Functions to handle button clicks
  const handleBrowseByGenre = () => {
    navigate('/browse-genre'); // Replace with your actual route
  };

  const handleGetRecommendation = () => {
    navigate('/recommendations'); // Replace with your actual route
  };

  // Send text to backend for mood analysis and genre suggestion
  // const fetchMoodAndGenre = async (text) => {
  //   try {
  //     const response = await fetch('http://127.0.0.1:8000/BookABook/analyze_mood/', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //       body: JSON.stringify({ text: text }),
  //     });
  
  //     if (!response.ok) {
  //       throw new Error(`HTTP error! Status: ${response.status}`);
  //     }
  
  //     const data = await response.json();
  //     setMood(data.mood);
  //     setSuggestedGenre(data.suggested_genre);
  //     setRecommendations(data.recommended_books); // Assume 'recommended_books' is part of the response
  //     //navigate('/recommendations', { state: { books: data.recommended_books } }); // Navigate with state
  //     console.log('Navigating with mood:', data.mood);
  //     navigate('/recommendations', { state: { books: data.recommended_books, mood: data.mood, genre: data.suggested_genre } });
  //   } catch (error) {
  //     console.error('There was a problem with the fetch operation:', error);
  //   }
  // };

  const fetchMoodAndGenre = async (text) => {
    setIsLoading(true); // Activate loading indicator
    try {
      const response = await fetch('http://127.0.0.1:8000/BookABook/analyze_mood/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setMood(data.mood);
      setSuggestedGenre(data.suggested_genre);
      setRecommendations(data.recommended_books); // Assume 'recommended_books' is part of the response
      console.log('Navigating with mood:', data.mood);
      navigate('/recommendations', { state: { books: data.recommended_books, mood: data.mood, genre: data.suggested_genre } });
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    } finally {
      setIsLoading(false); // Deactivate loading indicator
    }
  };

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      console.error("Speech recognition not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = (event) => {
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          const latestTranscript = event.results[i][0].transcript.trim();
          setTranscript(latestTranscript);
          fetchMoodAndGenre(latestTranscript);
        }
      }
    
    };

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onerror = (event) => console.error("Speech recognition error", event.error);

    if (isListening) {
      recognition.start();
    } else {
      recognition.stop();
    }

    return () => recognition.stop();
  }, [isListening]);

  const toggleListening = () => setIsListening(!isListening);

  return (
    <Paper elevation={3} style={{ padding: '20px', marginTop: '20px' }}>
      <Typography variant="h4" gutterBottom component="div" style={{ textAlign: 'center' }}>
        WELCOME
      </Typography>
      <Grid container spacing={2} justifyContent="center">
        <Grid item>
          <Button variant="contained" onClick={handleBrowseByGenre}>
            BROWSE BOOKS BY GENRE
          </Button>
        </Grid>
        <Grid item>
          <Button variant="contained" onClick={handleGetRecommendation}>
            GET RECOMMENDATION
          </Button>
        </Grid>
       
        <Grid item>
          <Button variant="contained" onClick={toggleListening} color={isListening ? "secondary" : "primary"}>
            {isListening ? 'Stop Listening' : 'Start Listening'}
            
          </Button>
        </Grid>

      </Grid>
      <Typography variant="h6" gutterBottom component="div" style={{ textAlign: 'center', marginTop: '20px' }}>
        "How do you feel today?"
      </Typography>
      <Grid container justifyContent="center" style={{ marginTop: '10px' }}>
        <Button variant="outlined" onClick={handleClickOpen}>
          Open Pop-up
        </Button>
      </Grid>

      {/* Dialog Pop-up */}
<Dialog open={open} onClose={handleClose} fullWidth maxWidth="xl">
  <DialogTitle>{"How do you feel today? Select three images that best represent your mood"}</DialogTitle>
  <DialogContent>
    <Grid container spacing={2} justifyContent="center">
      <Grid item>
        <img
          src={adventorous}
          alt="adventurous"
          onClick={() => handleImageSelect("adventurous")}
          style={{width: '200px',  height: '200px', border: selectedImages.includes("adventurous") ? '2px solid green' : '2px solid transparent'}}/>
            </Grid>
            <Grid item>
              <img src={cozy} alt="cozy" onClick={() => handleImageSelect("cozy")} style={{ width: '200px',  height: '200px', border: selectedImages.includes("cozy") ? '2px solid green' : '2px solid transparent'
 }} />
            </Grid>
            <Grid item>
              <img src={funny} alt="funny" onClick={() => handleImageSelect("funny")} style={{ width: '200px',  height: '200px',border: selectedImages.includes("funny") ? '2px solid green' : '2px solid transparent'
 }} />
            </Grid>
            <Grid item>
              <img src={happy2} alt="happy" onClick={() => handleImageSelect("happy")} style={{ width: '200px',  height: '200px',border: selectedImages.includes("happy") ? '2px solid green' : '2px solid transparent'
 }} />
            </Grid>
            <Grid item>
              <img src={love} alt="love" onClick={() => handleImageSelect("love")} style={{ width: '200px',  height: '200px',border: selectedImages.includes("love") ? '2px solid green' : '2px solid transparent'
 }} />
            </Grid>
            <Grid item>
              <img src={mysterious} alt="mysterious" onClick={() => handleImageSelect("mysterious")} style={{ wwidth: '200px',  height: '200px', border: selectedImages.includes("mysterious") ? '2px solid green' : '2px solid transparent'
 }} />
            </Grid>
            <Grid item>
              <img src={sad} alt="sad" onClick={() => handleImageSelect("sad")} style={{width: '200px',  height: '200px', border: selectedImages.includes("sad") ? '2px solid green' : '2px solid transparent'
 }} />
            </Grid>
            <Grid item>
              <img src={spring} alt="spring" onClick={() => handleImageSelect("spring")} style={{ width: '200px',  height: '200px',border: selectedImages.includes("spring") ? '2px solid green' : '2px solid transparent'
 }} />
            </Grid>
            <Grid item>
              <img src={thought_provoking} alt="thought provoking" onClick={() => handleImageSelect("thought provoking")} style={{ width: '200px',  height: '200px', border: selectedImages.includes("thought provoking") ? '2px solid green' : '2px solid transparent'
 }} />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Save
          </Button>
        </DialogActions>
      </Dialog>
      <Typography variant="h6" component="div" style={{ textAlign: 'center', marginTop: '20px' }}>
        Transcript: {transcript}
      </Typography>
      <Typography variant="h6" component="div" style={{ textAlign: 'center', marginTop: '20px' }}>
        Detected Mood: {mood}
      </Typography>
      <Typography variant="h6" component="div" style={{ textAlign: 'center', marginTop: '20px' }}>
        Suggested Genre: {suggestedGenre}
      </Typography>
      <Backdrop open={isLoading} style={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <CircularProgress color="inherit" />
      </Backdrop>
    </Paper>
  );
};

export default HomePage;
