<script lang="ts">
    import { onMount } from "svelte";
    import Books from "./Books.svelte";

    let books = { data: [] };

    onMount(async () => {
        const response = await fetch("http://localhost:8000/mirknig");
        books = await response.json();

        return books.data;
    });
</script>

{#await books}
    Loading ...
{:then books}
    {#each books.data as book}
        <div class="books">
            <div class="image">
                <img src={book.image} alt={book.book_title} width="150" />
            </div>
            <div class="book_data">
                <div>{book.author}</div>
                <div>{book.title}</div>
                <div>{book.language}</div>
                <div>{book.format}</div>
                <div>{book.pages}</div>
                <div>{book.file_size}</div>
                <div>{book.publisher}</div>
                <div>{book.year}</div>
                <div>{@html book.description}</div>
            </div>
        </div>
    {/each}
{:catch}
    Error ...
{/await}

<style>
    .books {
        display: flex;
        border: 1px solid pink;
    }

    .books > .image {
        min-width: 200px;
    }

    .book_data {
        padding: 0px 8px;
        display: flex;
        flex-direction: column;
        border: 1px solid rgb(19, 182, 92);
    }
</style>
