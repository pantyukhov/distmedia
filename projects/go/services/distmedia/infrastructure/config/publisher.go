package config

import "os"

type PublisherConfig struct {
	Address string `json:"address"`
}

func InitPublisherConfig() PublisherConfig {
	return NewPublisherConfig(os.Getenv("PUBLISHER_ADDRESS"))
}

func NewPublisherConfig(address string) PublisherConfig {
	return PublisherConfig{Address: address}
}
