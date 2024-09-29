import React, { useState, useEffect } from 'react';
import {
  Typography,
  TextField,
  Button,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Select,
  MenuItem,
  Grid,
  Box,
  Divider,
  InputLabel
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'

const UserProfileSetup = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    readingExperience: '',
    favoriteGenre: '',
    favoriteBook: '',
  });
  const [bookList, setbookList] = useState([])
  const [genreList, setGenreList] = useState([])


  const handleInputChange = (e) => {
    console.log(e.target)
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form Data:', formData);
    
    navigate('/');
  };

  const saveBooksAndGenres = () => {
    let user_id = sessionStorage. getItem('user_id')
    axios.post(`http://127.0.0.1:8000/BookABook/save_favorite_books_and_genres/?user_id=${user_id}`,{
      "favorite_books": `${formData.favoriteBook}`,
      "favorite_genres": `${formData.favoriteGenre}`,
    }  
  ).then((result) => console.log(result))
  }

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/BookABook/get_all_books').then((result) => 
    setbookList(result.data)
  )
    axios.get('http://127.0.0.1:8000/BookABook/get_all_genres').then((result) => setGenreList(result.data))
  },[])

  return (
    <Box p={3}>
      <Typography variant="h5" gutterBottom>
        User Setup
      </Typography>
      <Divider />
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3} mt={3}>
          <Grid item xs={12}>
            <FormControl component="fieldset">
              <FormLabel component="legend">1. Would you consider yourself an:</FormLabel>
              <RadioGroup
                row
                name="readingExperience"
                value={formData.readingExperience}
                onChange={handleInputChange}
              >
                <FormControlLabel value="expert" control={<Radio />} label="Expert Reader" />
                <FormControlLabel value="average" control={<Radio />} label="Average Reader" />
                <FormControlLabel value="first-time" control={<Radio />} label="First Time Reader" />
              </RadioGroup>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <FormControl fullWidth>
              <InputLabel>2. Which is your favorite genre?</InputLabel>
              <Select
                label="Favorite Genre"
                name="favoriteGenre"
                value={formData.favoriteGenre}
                onChange={handleInputChange}
              >
                {console.log(genreList)}
                {
                  genreList?.genres?.length > 0 ? genreList?.genres.map(genre =>
                  <MenuItem value = {genre}>{genre}</MenuItem>
                 
                  )
                  : <MenuItem>No Genre found</MenuItem>
              }
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12}>
            <FormControl fullWidth>
              <InputLabel>3. Select your Favorite Book?</InputLabel>
              <Select
                label="Favorite Book"
                name="favoriteBook"
                value={formData.favoriteBook}
                onChange={handleInputChange}
              >
                {
                  bookList?.books?.length > 0 ? bookList?.books.map(book =>
                  <MenuItem value = {book}>{book}</MenuItem>
                 
                  )
                  : <MenuItem>No books found</MenuItem>
              }
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <Button variant="contained" color="primary" type="submit" onClick={saveBooksAndGenres}>
              Save
            </Button>
          </Grid>
        </Grid>
      </form>
    </Box>
  );
};

export default UserProfileSetup;
