import React from "react";

export function ArticleList({ articles, onSelect }) {
  if (!articles || articles.length === 0) {
    return <p>No articles found.</p>;
  }

  return (
    <ul>
      {articles.map((article) => (
        <li key={article.id}>
          <button type="button" onClick={() => onSelect(article.id)}>
            {article.title}
          </button>
        </li>
      ))}
    </ul>
  );
}
