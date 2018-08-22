package main

import (
	_ "bytes"
	_ "github.com/ethereum/go-ethereum/common/compiler"
	"github.com/loomnetwork/go-loom/plugin"
	contract "github.com/loomnetwork/go-loom/plugin/contractpb"
	_ "text/template"
	"types"
)

type ContractVars struct {
	Token *types.TokenMeta
}

type TokenFactory struct {
}

func (e *TokenFactory) Init(ctx contract.Context, req *plugin.Request) error {
	return nil
}

func (c *TokenFactory) Meta() (plugin.Meta, error) {
	return plugin.Meta{
		Name:    "TokenFactory",
		Version: "0.0.1",
	}, nil
}

func (c *TokenFactory) GetMsg(ctx contract.StaticContext, req *types.MapEntry) (*types.MapEntry, error) {
	var result types.MapEntry
	if err := ctx.Get([]byte(req.Key), &result); err != nil {
		return nil, err
	}
	return &result, nil
}

//func (c *TokenFactory) PrepareToken(ctx contract.Context, meta *types.TokenMeta) (evmHex string) {
//	t := template.Must(template.New(".token.sol.template").ParseFiles("./solidity/token.sol.template"))
//	buf := new(bytes.Buffer)
//	t.Execute(buf, ContracytVars{
//		Token: meta,
//	})
//
//	contracts, _ := compiler.CompileSolidityString("0.4.21", buf.String())
//
//	return contracts["Token"].Code
//}

var Contract plugin.Contract = contract.MakePluginContract(&TokenFactory{})

func main() {

	plugin.Serve(Contract)
}
