package service

import (
	"context"
	"github.com/pantyukhov/distmedia/projects/pubsub/pkg/domain/entity"
)

type ArticlePublisher interface {
	PublishArticle(ctx context.Context, topic string, req *entity.Article) error
}
