![Wordcloud](figures/WordFreq.png)

<details>
    <summary><h2>Español</h2></summary>


# Tienda Steam 2024: Selecciones destacadas y reseñas 💨

## Acerca del conjunto de datos

### Descripción general:

Sumérgete en el pulso de la Tienda Steam con nuestro conjunto de datos **«Clasificación de poder de la Tienda Steam 2024: Selecciones destacadas y reseñas»**. Esta colección compacta pero potente ofrece una instantánea de los títulos más comentados de 2024, incluyendo precios, descuentos y la opinión colectiva de la comunidad gamer. Extraído de forma ética, este conjunto representa la vibrante cultura de los videojuegos en Steam.

### Aplicaciones de la ciencia de datos:

* **Análisis de tendencias**: Identifica patrones en la popularidad y precios de los juegos.
* **Análisis de opiniones**: Evalúa la percepción general mediante las reseñas.
* **Análisis de mercado**: Comprende relaciones entre precios, descuentos y calificaciones.
* **Proyectos de visualización**: Crea gráficos impactantes sobre insights clave.

---

## Descripción de columnas:

| Columna          | Descripción                               |
| ---------------- | ----------------------------------------- |
| `Title`          | Nombre del juego.                         |
| `Description`    | Breve descripción del título.             |
| `Price`          | Precio listado en Steam.                  |
| `SalePercentage` | Porcentaje de descuento actual.           |
| `RecentReviews`  | Reseñas recientes (sentimiento general).  |
| `AllReviews`     | Reseñas acumuladas (sentimiento general). |

---

## Visualizaciones

### Distribución de las categorías de juegos

![Distribución de Categorías](figures/DistCatJuego.png)

### Distribución de los descuentos

![Descuentos](figures/DistDesc.png)

### Distribución de los precios

![Precios](figures/DistPrec.png)

### Distribución de precios por categoría

![Precios por categoría](figures/DistPrecPerCat.png)

### Distribución de reseñas generales

![Reseñas](figures/DistResenas.png)

### Distribución de reseñas recientes por categoría

![Reseñas por Categoría](figures/DistResenasRecientesPerCat.png)

### Nube de palabras de descripciones

![Wordcloud](figures/WordFreq.png)

---

## Conclusión

* **Distribución de categorías**: Predominan los juegos sin categoría clara (`Unknown`), seguidos de RPG y acción. Las categorías puzzle, estrategia y aventura tienen menor representación.
* **Precios**: La mayoría de juegos tienen precios entre \$10 y \$30 USD, con algunos outliers.
* **Descuentos**: Se observan descuentos de hasta el 80%, con un rango común cercano al 30%.
* **Reseñas**: Las reseñas "Very Positive" dominan ampliamente. Muy pocos juegos tienen reseñas mixtas o negativas.
* **Precios por categoría**: RPG y aventura muestran los precios más altos en promedio; puzzle es la categoría con precios más bajos.
* **Reseñas por categoría**: Los juegos "Unknown" y RPG tienen la mayor cantidad de reseñas positivas recientes.
* **Descripción de juegos**: Palabras como `world`, `new`, `action`, y `play` destacan en la nube de palabras, indicando un enfoque en experiencias inmersivas.

</details>

<details>
    <summary><h2>English</h2></summary>

    # Steam Store 2024: Featured Picks and Reviews 💨

## About the Dataset

### Overview

Dive into the pulse of the Steam Store with our dataset **"Steam Store Power Ranking 2024: Featured Picks and Reviews"**. This compact but rich dataset captures the most talked-about games of 2024, providing insights into pricing, community sentiment, and trends. Ethically sourced, it encapsulates the vibrant gaming ecosystem and market dynamics of Steam.

### Data Science Applications

- **Trend analysis**: Spot popularity and pricing patterns over time.
- **Sentiment analysis**: Quantify community perception through reviews.
- **Market analytics**: Explore correlations between pricing, sales, and ratings.
- **Visualization projects**: Create engaging charts and visual narratives.

---

## Column Descriptions

| Column           | Description                                  |
|------------------|----------------------------------------------|
| `Title`          | Game title.                                  |
| `Description`    | Brief summary of the game.                   |
| `Price`          | Game price listed on Steam.                  |
| `SalePercentage` | Discount percentage if available.            |
| `RecentReviews`  | Sentiment from recent reviews.               |
| `AllReviews`     | Overall review sentiment.                    |

---

## Visualizations

- **Category Distribution**  
  ![Category Distribution](figures/DistCatJuego.png)

- **Discount Distribution**  
  ![Discounts](figures/DistDesc.png)

- **Price Distribution**  
  ![Prices](figures/DistPrec.png)

- **Price by Category**  
  ![Price by Category](figures/DistPrecPerCat.png)

- **Overall Review Distribution**  
  ![Reviews](figures/DistResenas.png)

- **Recent Reviews by Category**  
  ![Recent Reviews by Category](figures/DistResenasRecientesPerCat.png)

- **Description WordCloud**  
  ![WordCloud](figures/WordFreq.png)

---

## Conclusion

- **Category Distribution**: Most games are labeled as `Unknown`, followed by RPG and Action titles.
- **Price Trends**: Most games fall between $10–30, with some exceptions.
- **Discounts**: Significant sales are common, with a peak around 30%.
- **Reviews**: Majority of games receive "Very Positive" reviews.
- **Price by Category**: RPG and Adventure titles are more expensive; Puzzle games are cheaper.
- **Review Trends**: RPG and Unknown games have more frequent recent positive reviews.
- **Description Themes**: Keywords such as `world`, `play`, `action`, and `new` are dominant.

---

## 🔧 How to Run

```bash
pip install -r requirements.txt

python src/steam.py
```

</details>