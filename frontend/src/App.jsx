import React, { useEffect, useState } from "react";
import { fetchArticles, fetchArticleById } from "./api.js";
import { ArticleList } from "./components/ArticleList.jsx";
import { ArticleDetail } from "./components/ArticleDetail.jsx";

export default function App() {
  const [articles, setArticles] = useState([]);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [showFeaturedOnly, setShowFeaturedOnly] = useState(false);
  const [error, setError] = useState(null);

  // Load articles whenever the "show featured" toggle changes

  useEffect(() => {
    let isCancelled = false;

    async function load() {
      try {
        setError(null);
        const data = await fetchArticles({
          featured: showFeaturedOnly ? true : undefined,
        });
        if (!isCancelled) {
          setArticles(data);
        }
      } catch (e) {
        if (!isCancelled) {
          setError(e.message);
        }
      }
    }

    load();

    return () => {
      isCancelled = true;
    };
  }, [showFeaturedOnly]); // ← bug here

  const handleSelectArticle = async (articleId) => {
    try {
      setError(null);
      const data = await fetchArticleById(articleId);
      setSelectedArticle(data);
    } catch (e) {
      setError(e.message);
    }
  };

  const handleToggleFeatured = (e) => {
    setShowFeaturedOnly(e.target.checked);
    setSelectedArticle(null);
  };

  return (
    <div style={{ display: "flex", gap: "1rem" }}>
      <section style={{ flex: 1 }}>
        <h1>News Articles</h1>
        <label>
          <input
            type="checkbox"
            checked={showFeaturedOnly}
            onChange={handleToggleFeatured}
          />
          Show only featured
        </label>

        {error && (
          <p role="alert" style={{ color: "red" }}>
            {error}
          </p>
        )}

        <ArticleList articles={articles} onSelect={handleSelectArticle} />
      </section>

      <section style={{ flex: 1 }}>
        <h2>Details</h2>
        <ArticleDetail article={selectedArticle} />
      </section>
    </div>
  );
}
