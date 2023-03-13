package broker

import (
	"context"
	"github.com/pantyukhov/distmedia/projects/pubsub/pkg/domain/entity"
)

type ArticleSub interface {
	SubscribeArticle(ctx context.Context, req *entity.Article) error
}
