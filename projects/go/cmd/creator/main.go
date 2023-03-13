package main

import (
	"context"
	"github.com/joho/godotenv"
	"github.com/pantyukhov/distmedia/projects/pubsub/services/distmedia"
	"github.com/urfave/cli/v2"
	"os"
)

func init() {
	godotenv.Load(".env")
}

func main() {

	ctx := context.Background()

	app := &cli.App{
		Commands: []*cli.Command{
			{
				Name:    "start",
				Aliases: []string{"s"},
				Usage:   "Start server",
				Action: func(cCtx *cli.Context) error {
					return distmedia.Start(ctx)
				},
			},
		},
	}

	if err := app.Run(os.Args); err != nil {
		panic(err)
	}
}
