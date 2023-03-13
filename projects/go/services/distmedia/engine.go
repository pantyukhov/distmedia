package distmedia

import (
	"context"
	"github.com/gin-gonic/gin"
	"github.com/pantyukhov/distmedia/projects/pubsub/services/distmedia/routes"
)

type Engine struct {
	publisherRoute *routes.PublisherRoute
	//broker service.ArticlePub
}

func NewEngine(publisherRoute *routes.PublisherRoute) *Engine {
	return &Engine{publisherRoute: publisherRoute}
}

func (e *Engine) initRoutes() *gin.Engine {
	router := gin.Default()
	router.POST("/api/publish", e.publisherRoute.PublishArticle)

	return router
}

func (e *Engine) Start(ctx context.Context) error {
	router := e.initRoutes()

	return router.Run("localhost:9090")
}
