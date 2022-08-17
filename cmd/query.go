/*
Copyright © 2022 Paul Norman <osm@paulnorman.ca>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
*/
package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

// queryCmd represents the query command
var queryCmd = &cobra.Command{
	Use:   "query",
	Short: "Generates SQL queries for tiles",
	Long: `Query processes a tilekiln configuration and prints, to stdout, the
query needed to generate a tile.

This enables manually running the query to debug, particularly with EXPLAIN.`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("query called")
	},
}

func init() {
	rootCmd.AddCommand(queryCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	queryCmd.PersistentFlags().StringP("tile", "t", "", "z/x/y of tile to generate")
	queryCmd.MarkPersistentFlagRequired("tile")
	queryCmd.PersistentFlags().StringP("layer", "l", "", "Tile layer generator to generate SQL for. If missing, all layers are generated.")
	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// queryCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
