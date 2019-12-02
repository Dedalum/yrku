<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithFaker;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

use App\User;

class BookControllerTest extends TestCase
{
    use RefreshDatabase;

    /**
     * Ensure guests cannot get the book list
     *
     * @return void
     */
    public function testGuestsCannotGetBooks()
    {
        $this->get('/books')
            ->assertStatus(302)
            ->assertLocation('/login');
    }

    /**
     * Ensure authenticated users get the book list
     *
     * @return void
     */
    public function testAuthenticatedUsersCanGetBooks()
    {
        $user = factory(User::class)->make();

        $this->actingAs($user)->get('/books')
            ->assertStatus(200);
    }

    /**
     * Ensure authenticated users can export the book list in CSV format
     *
     * @return void
     */
    public function testAuthenticatedUsersCanExportCSVBooks()
    {
        $user = factory(User::class)->make();

        $response = $this->actingAs($user)->get('/books?format=csv')
            ->assertStatus(200);
       
        //Storage::disk('local')->assertExists('storage/app/public/books.csv');
    }

    /**
     * Ensure authenticated users can export the book list in XML format
     *
     * @return void
     */
    public function testAuthenticatedUsersCanExportXMLBooks()
    {
        $user = factory(User::class)->make();

        $response = $this->actingAs($user)->get('/books?format=xml')
            ->assertStatus(200);
    }

    /**
     * Ensure authenticated users can add books
     *
     * @return void
     */
    public function testAuthenticatedUsersCanAddBook()
    {
        $user = factory(User::class)->make();
        $book = [
            'title' => 'Test Title',
            'author' => 'Test Author'
        ];
        $this->actingAs($user)->post('/books', $book)
            ->assertStatus(302)
            ->assertLocation('/books');

        $this->get('/book/1')
            ->assertStatus(200);
    }

    /**
     * Ensure authenticated users can delete books
     *
     * @return void
     */
    public function testAuthenticatedUserCanDeleteBook()
    {
        $user = factory(User::class)->make();

        $book = [
            'title' => 'Test Title 2',
            'author' => 'Test Author 2'
        ];
        $this->actingAs($user)->post('/books', $book)
            ->assertStatus(302)
            ->assertLocation('/books');

        $this->get('/book/2')
            ->assertStatus(200);
        $data = [
            '_method' => 'DELETE'
        ];
        $this->actingAs($user)->post('/book/2', $data)
            ->assertStatus(302)
            ->assertLocation('/books');

        $this->get('/book/2')
            ->assertStatus(404);
    }
}
