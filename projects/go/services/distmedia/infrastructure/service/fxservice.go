package service

import (
	brokerDomain "github.com/pantyukhov/distmedia/projects/pubsub/services/distmedia/domain/service"
	"go.uber.org/fx"
)

var Module = fx.Options(
	fx.Provide(NewArticleService),
	fx.Provide(func(s *ArticleService) brokerDomain.ArticlePublisher {
		return s
	}),
)
