package main

import (
	"github.com/loomnetwork/go-loom"
	"github.com/loomnetwork/go-loom/builtin/types/coin"
	"github.com/loomnetwork/go-loom/plugin"
	contract "github.com/loomnetwork/go-loom/plugin/contractpb"
	"github.com/loomnetwork/go-loom/types"
	"text/template"
	"bytes"
	"github.com/ethereum/go-ethereum/common/compiler"
)

type TokenMeta struct {
	Name, Symbol            string
	Decimals, InitialSupply int
}

type ContracytVars struct {
	Token TokenMeta
}

type TokenFactory struct {
}

var coinContractKey = []byte("coincontract")

func transfer(ctx contract.Context, to loom.Address, amount *loom.BigUInt) error {
	req := &coin.TransferRequest{
		To:     to.MarshalPB(),
		Amount: &types.BigUInt{Value: *amount},
	}

	coinAddr, err := ctx.Resolve("coin")
	if err != nil {
		return err
	}
	return contract.Call(ctx, coinAddr, req, nil)
}

func (c *TokenFactory) Meta() (plugin.Meta, error) {
	return plugin.Meta{
		Name:    "token_factory",
		Version: "0.1.0",
	}, nil
}

func (c *TokenFactory) PrepareToken(ctx contract.Context, name string, symbol string, decimals, supply int) (evmHex string) {
	t := template.Must(template.New(".token.sol.template").ParseFiles("./solidity/token.sol.template"))
	buf := new(bytes.Buffer)
	t.Execute(buf, ContracytVars{
		Token: TokenMeta{
			Name:          name,
			Symbol:        symbol,
			Decimals:      decimals,
			InitialSupply: supply,
		},
	})

	contracts, _ := compiler.CompileSolidityString("0.4.21", buf.String())

	return contracts["Token"].Code
}

var Contract plugin.Contract = contract.MakePluginContract(&TokenFactory{})

func main() {

	plugin.Serve(Contract)
}
