// import React, { useState, useEffect } from 'react';
// import { Typography, Select, MenuItem, FormControl, InputLabel, List, ListItem } from '@mui/material';
// import axios from "axios"

// const BookGenreSelector = () => {
//   const [selectedGenre, setSelectedGenre] = useState('');
//   const [books, setBooks] = useState([]);
//   const [genreList, setgenreList] = useState([])

//   useEffect(() => {
//     axios.get("http://127.0.0.1:8000/BookABook/get_all_genres").then((res) => {
//       setgenreList(res)
//     })
//     const fetchBooks = async () => {

//       const booksFromDb = [
//         { title: 'Book 1' },
//         { title: 'Book 2' },
//         { title: 'Book 3' }
//         // This would be replaced by the actual response from the database
//       ];
//       setBooks(booksFromDb);
//     };

//     if (selectedGenre) {
//       fetchBooks();
//     }
//   }, [selectedGenre]);

//   const handleGenreChange = (event) => {
//     setSelectedGenre(event.target.value);
//   };

//   return (
//     <div>
//       <FormControl fullWidth>
//         <InputLabel id="genre-select-label">Select a Genre</InputLabel>
//         <Select
//           labelId="genre-select-label"
//           id="genre-select"
//           value={selectedGenre}
//           label="Select a Genre"
//           onChange={handleGenreChange}
//           placeholder="from the db"
//         >
//           {/* Replace these with actual genres fetched from the database */}
//           <MenuItem value="Historical Fiction">Fiction</MenuItem>
//           <MenuItem value="Novella">Non-Fiction</MenuItem>
//           <MenuItem value="Fantasy">Fantasy</MenuItem>
//           <MenuItem value="Mystery">Mystery</MenuItem>
//           {/* etc. */}
//         </Select>
//       </FormControl>
//       <Typography variant="h6" component="div" sx={{ mt: 2 }}>
//         Books
//       </Typography>
//       <List>
//         {books.map((book, index) => (
//           <ListItem key={index}>{book.title}</ListItem>
//         ))}
//       </List>
//     </div>
//   );
// };

// export default BookGenreSelector;


import React, { useState, useEffect } from 'react';
import { Typography, Select, MenuItem, FormControl, InputLabel, List, ListItem } from '@mui/material';
import axios from "axios";

const BookGenreSelector = () => {
  const [selectedGenre, setSelectedGenre] = useState('');
  const [books, setBooks] = useState([]);
  const [genreList, setGenreList] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/BookABook/get_all_genres")
      .then((response) => {
        if (Array.isArray(response.data)) {
          setGenreList(response.data);
        } else if (response.data.genres && Array.isArray(response.data.genres)) {
          setGenreList(response.data.genres);
        } else {
          setGenreList([]);
        }
      })
      .catch((error) => {
        console.error('Error fetching genres:', error);
        setGenreList([]);
      });
  }, []);

  useEffect(() => {
    if (selectedGenre) {
      fetchBooks(selectedGenre);
    }
  }, [selectedGenre]);

  const fetchBooks = async (genre) => {
    // Adjusted URL to include query parameter for genre
    axios.get(`http://127.0.0.1:8000/BookABook/book/?genre=${genre}`)
      .then(response => {
        if (response.data && Array.isArray(response.data)) {
          setBooks(response.data);
        } else {
          setBooks([]); // Clear the books if the response is not as expected
        }
      })
      .catch(error => {
        console.error('Error fetching books:', error);
        setBooks([]); // Clear the books on error
      });
  };

  const handleGenreChange = (event) => {
    setSelectedGenre(event.target.value);
  };

  return (
    <div>
      <FormControl fullWidth>
        <InputLabel id="genre-select-label">Select a Genre</InputLabel>
        <Select
          labelId="genre-select-label"
          id="genre-select"
          value={selectedGenre}
          label="Select a Genre"
          onChange={handleGenreChange}
        >
          {genreList?.length > 0 && genreList.map((genre, index) => (
            <MenuItem key={index} value={genre}>{genre}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <Typography variant="h6" component="div" sx={{ mt: 2 }}>
        Books
      </Typography>
      <List>
        {books.map((book, index) => (
          <ListItem key={index}>{book.title}</ListItem>
        ))}
      </List>
    </div>
  );
};

export default BookGenreSelector;
