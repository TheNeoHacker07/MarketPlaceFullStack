import { useState } from "react";
import Main from "./pages/Main";
import Details from "./pages/Details";
import Login from "./pages/Login";
import Layout from "./Layout";
import Data from "./pages/Data";
import {Route, createBrowserRouter, createRoutesFromElements, RouterProvider} from "react-router-dom";


const products = [
    { id: 1, name: "Laptop", price: 1200, narrator: "John" },
    { id: 2, name: "Smartphone", price: 800, narrator: "Alice" },
    { id: 3, name: "Headphones", price: 150, narrator: "Bob" },
    { id: 4, name: "Smartwatch", price: 200, narrator: "Emma" },
    { id: 5, name: "Tablet", price: 400, narrator: "Mike" },
    { id: 6, name: "MAC M4", price: 1500, narrator: "Neo" },
    { id: 7, name: "MAC M4", price: 1500, narrator: "Neo" },
    { id: 8, name: "MAC M4", price: 1500, narrator: "Neo" },
    { id: 9, name: "MAC M4", price: 1500, narrator: "Neo" },
    { id: 10, name: "MAC M4", price: 1500, narrator: "Neo" },
    { id: 11, name: "MAC M4", price: 1500, narrator: "Neo" },
    { id: 12, name: "MAC M4", price: 1500, narrator: "Neo" }
  ];




function App() {
  const [login, setLogin] = useState("")

  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route path="/" element={<Layout/>}>
        <Route path="home" element={<Main/>}/>
        <Route path="sign-in" element={<Login login={login} setLogin={setLogin}/>}/>
        <Route path="product/:id" element={<Details products={products}/>}/>
        <Route path="about" element={<Data/>}/>
      </Route>
    )
  )

  return (
    <RouterProvider router={router}/>
  );
}


export default App;
