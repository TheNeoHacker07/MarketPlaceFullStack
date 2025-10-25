import React from 'react'

import styles from "./Products.module.css"
import { useNavigate } from 'react-router-dom';


const Products = (props) => {

    const {products} = props;

    const navigate = useNavigate();
    const viewProduct = id => navigate(`/product/${id}`)

    return (
    <>
        <div className={styles.preview_data}>
            <h1 style={{ textAlign: 'center', marginTop: '50px' }}>Products List</h1>
            <button className={styles.fetchButton} >new products</button>
        </div>

        <div className={styles.productContent}>
            {products.map(product => (
              <div className={styles.product}  key={product.id}>
                <h2>{product.name}</h2>
                <div className={styles.productDataContent}>
                  <p>Price: ${product.price}</p>
                  <p>Narrator: {product.narrator}</p>
                </div>
                <button className={styles.button} onClick={() => viewProduct(product.id)}>View Product</button>
              </div>
            ))}
        </div>

    </>
  )
}

export default Products


