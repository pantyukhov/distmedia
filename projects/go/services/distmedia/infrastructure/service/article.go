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
	pubSub *pubsub.PubSub
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

	return &ArticleService{
		pubSub: gossipSub,
	}
}

func (s *ArticleService) PublishArticle(ctx context.Context, topic string, req *entity.Article) error {
	t, err := s.pubSub.Join(topic)
	if err != nil {
		panic(err)
	}

	data, err := req.Marshal()
	if err != nil {
		return err
	}

	go func() {
		t.Subscribe()
	}()

	return t.Publish(context.Background(), data)

}
