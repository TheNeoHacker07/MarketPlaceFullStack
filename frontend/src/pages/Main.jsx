import React from 'react';
import Products from '../components/Products';
import Footer from '../components/Footer';

const Main = () => {
  
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

  return (
    <>
      <Products products={products}/>
      <Footer/>
    </>
  );
};

export default Main;
