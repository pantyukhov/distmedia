package entity

import "encoding/json"

type Article struct {
	Content string
}

func NewArticle(content string) *Article {
	return &Article{Content: content}
}

func (a *Article) Marshal() ([]byte, error) {
	return json.Marshal(a)
}
