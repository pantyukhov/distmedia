package service

import (
	"context"
	"github.com/pantyukhov/distmedia/projects/pubsub/pkg/domain/entity"
)

type ArticlePublisher interface {
	PublishArticle(ctx context.Context, req *entity.Article) error
}
