package models

import "github.com/pantyukhov/distmedia/projects/pubsub/pkg/domain/entity"

type CreateArticleReq struct {
	Article entity.Article
	Topic   string
}

func NewCreateArticleReq(article entity.Article, topic string) *CreateArticleReq {
	return &CreateArticleReq{Article: article, Topic: topic}
}
