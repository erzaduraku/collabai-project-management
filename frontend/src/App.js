import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<h1>Home Page</h1>} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;