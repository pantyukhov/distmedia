package service

import (
	"context"
	"fmt"
	"github.com/libp2p/go-libp2p"
	pubsub "github.com/libp2p/go-libp2p-pubsub"
	"github.com/pantyukhov/distmedia/projects/pubsub/pkg/domain/entity"
	"github.com/pantyukhov/distmedia/projects/pubsub/services/distmedia/infrastructure/config"
)

type ArticleService struct {
	topic *pubsub.Topic
}

func NewArticleService(ctx context.Context, publisherConfig config.PublisherConfig) *ArticleService {
	host, err := libp2p.New(libp2p.ListenAddrStrings("/ip4/0.0.0.0/tcp/0"))
	if err != nil {
		panic(err)
	}

	fmt.Printf("host ID %s\n", host.ID().Pretty())
	fmt.Printf("following are the assigned addresses\n")
	for _, addr := range host.Addrs() {
		fmt.Printf("%s\n", addr.String())
	}
	fmt.Printf("\n")

	// create a new PubSub service using the GossipSub router
	gossipSub, err := pubsub.NewGossipSub(ctx, host)
	if err != nil {
		panic(err)
	}

	room := publisherConfig.Address
	topic, err := gossipSub.Join(room)
	if err != nil {
		panic(err)
	}

	return &ArticleService{
		topic: topic,
	}
}

func (s *ArticleService) PublishArticle(ctx context.Context, req *entity.Article) error {
	data, err := req.Marshal()
	if err != nil {
		return err
	}

	return s.topic.Publish(ctx, data)

}
