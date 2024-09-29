// import React from 'react';
// import { HashRouter as Router, Routes, Route } from 'react-router-dom';
// import { Container, AppBar, Toolbar, Typography } from '@mui/material';
// import LoginPage from './Components/LoginPage';
// import HomePage from './Components/HomePage';
// import RegisterPage from './Components/Register';
// import UserProfileSetup from './Components/UserProfileSetup';
// import BookGenreSelector from './Components/BookGenreSelector';
// import BookRecommendations from './Components/BookRecommendations';

// const App = () => {
//   return (
//     <Router>
//       <div>
//         <AppBar position="static">
//           <Toolbar>
//             <Typography variant="h6">bookAbook</Typography>
//           </Toolbar>
//         </AppBar>
//           <Container maxWidth="lg" style={{ marginTop: '20px' }}>
//           <Routes>
//             <Route exact path="/" element={<HomePage />} />
//             <Route exact path="/login" element={<LoginPage />} />
//             <Route exact path="/register" element={<RegisterPage />} />
//             <Route exact path = "/user-setup" element = {<UserProfileSetup/>} />
//             <Route exact path="/browse-genre" element={<BookGenreSelector />} />
//             <Route exact path="/recommendations" element={<BookRecommendations />} />

//           </Routes>
//           </Container>
//       </div>
//     </Router>
//   );
// };

// export default App;


import React from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { Container, AppBar, Toolbar, Typography } from '@mui/material';
import LoginPage from './Components/LoginPage';
import HomePage from './Components/HomePage';
import RegisterPage from './Components/Register';
import UserProfileSetup from './Components/UserProfileSetup';
import BookGenreSelector from './Components/BookGenreSelector';
import BookRecommendations from './Components/BookRecommendations';

const App = () => {
  return (
    <Router>
      <div>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6">bookAbook</Typography>
          </Toolbar>
        </AppBar>
          <Container maxWidth="lg" style={{ marginTop: '20px' }}>
          <Routes>
            <Route exact path="/" element={<HomePage />} />
            <Route exact path="/login" element={<LoginPage />} />
            <Route exact path="/register" element={<RegisterPage />} />
            <Route exact path = "/user-setup" element = {<UserProfileSetup/>} />
            <Route exact path="/browse-genre" element={<BookGenreSelector />} />
            <Route exact path="/recommendations" element={<BookRecommendations />} />

          </Routes>
          </Container>
      </div>
    </Router>
  );
};

export default App;
