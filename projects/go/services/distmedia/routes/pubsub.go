package routes

import (
	"github.com/gin-gonic/gin"
	"github.com/pantyukhov/distmedia/projects/pubsub/services/distmedia/domain/service"
	"github.com/pantyukhov/distmedia/projects/pubsub/services/distmedia/routes/models"
	"net/http"
)

type PublisherRoute struct {
	articlePublisher service.ArticlePublisher
}

func NewPublisherRoute(articlePublisher service.ArticlePublisher) *PublisherRoute {
	return &PublisherRoute{articlePublisher: articlePublisher}
}

func (p *PublisherRoute) PublishArticle(c *gin.Context) {
	var req models.CreateArticleReq

	if err := c.BindJSON(&req); err != nil {
		return
	}

	err := p.articlePublisher.PublishArticle(c, &req.Article)
	if err != nil {
		_ = c.AbortWithError(http.StatusBadRequest, err).SetType(gin.ErrorTypeBind)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		//"hash": h,
	})

}
