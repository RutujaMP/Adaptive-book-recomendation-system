import React, { useEffect, useState } from 'react';
import { Card, CardActionArea, CardContent, Typography } from '@mui/material';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import StarRating from './StarRating'; // Assuming you've placed the StarRating component in a separate file

axios.defaults.withCredentials = true;
let user_id = sessionStorage. getItem('user_id')
console.log("user_id",user_id)
const BookRecommendations = () => {
  const [allrecommendation, setAllrecommendation] = useState([]);
  const location = useLocation();
  const { books, mood, genre } = location.state || {};

  const fetchRecommendations = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/BookABook/get_recommendations/?user_id=${user_id}`, {
      withCredentials: true
    });
    setAllrecommendation(response.data);
  } catch (error) {
    console.error("Error fetching recommendations:", error);
  }
};


  useEffect(() => {
    if (books && books.length > 0) {
      // If data is received from useLocation, store it in allrecommendation state
      setAllrecommendation(books);
    } else {
      // If data is not received from useLocation, fetch recommendations from API
      fetchRecommendations();
    }
  }, [books]);

  const handleBookClick = (bookId) => {
    console.log(`Book with ID ${bookId} was clicked.`);
  };

  const handleRatingChange = async (bookId, rating) => {
    console.log("user id ",user_id)
    try {
      // Send rating details to API
      console.log(bookId)
      await axios.post(`http://127.0.0.1:8000/BookABook/save_rating/?user_id=${user_id}`, {'book_id' : bookId, 'rating' : rating});
      console.log(`Rating ${rating} sent for book with ID ${bookId}`);
    } catch (error) {
      console.error("Error sending rating:", error);
    }
  };

  return (
    <Card elevation={3} sx={{ margin: 2 }}>
      
      {/* Display Mood and Genre */}
      <Typography variant="h6" gutterBottom sx={{ mt: 2, textAlign: 'center' }}>Detected Mood: {mood}</Typography>
      <Typography variant="h6" gutterBottom sx={{ textAlign: 'center' }}>Suggested Genre: {genre}</Typography>
      <CardContent>
        <Typography variant="h5" component="div">
          Books We Recommend:
        </Typography>
        {console.log(allrecommendation)}
        {allrecommendation?.recommendations?.length > 0 && allrecommendation?.recommendations.map((book, index) => (
          <>
          {console.log(book)}
          <CardActionArea key={index} onClick={() => handleBookClick(book.id)} sx={{ marginTop: 2 }}>
            <Typography variant="h6" gutterBottom>
              Title: {book.title}
            </Typography>
            <Typography variant="body1" gutterBottom>
              Author: {book.author}
            </Typography>
            <Typography variant="body1" gutterBottom>
              Genres: {book.genres.join(', ')}
            </Typography>
            <StarRating
              value={book.rating || 0} // Assuming each book object has a rating property
              onChange={(newValue) => handleRatingChange(book.id, newValue)}
            />
          </CardActionArea>
          </>
        ))}
      </CardContent>
    </Card>
  );
};

export default BookRecommendations;
